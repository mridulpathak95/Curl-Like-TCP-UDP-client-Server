import socket
import os
import time
from threading import Thread
verbose=False

def myheader(val,lenth):
    txt1="HTTP/1.0 "+val[2]+"\r\n"
    date2="Date: "+val[3]+"\r\n"
    x=socket.gethostname()
    server="Server:"+x+"\r\n"
    clen="Content-Length: "+str(lenth)+"\r\n"
    txt2="Access-Control-Allow-Origin: *\r\n"
    txt3="Access-Control-Allow-Credentials: true\r\n"
    txt4="\r\n".join(val[0])
    return txt1+date2+server+clen+txt2+txt3+txt4



def security(value):
    if verbose:
        print("CHECKING SECURITY FOR FILE REQUEST")
    vals=value[0].split(" ")[1][1:]
    if len(vals)<1:
        return "index.html","200 OK"
    elif vals[0:3]=="../":
        return "","400 BAD REQUEST"
    else:
        return vals,"200 OK"

def security2(value):
    if verbose:
        print("CHECKING SECURITY FOR FILE REQUEST")
    vals=value[0].split(" ")[1][1:]
    if len(vals)<1 or vals[0:3]=="../":
        return "","400 BAD REQUEST"
    else:
        return vals,"200 OK"

def contenttype(value):
    output=""
    for i in value:
        if(i[0:12].lower()=="content-type"):
            output= i[13:].lower()
            break;

    if output=="":
        output="txt"
        if verbose:
            print("Content-Type Not Found.. Default Content Type Text")
    return output             

def callpost(value,Path,address):
    
        if verbose:
            print("Request Type : POST request")
        got=value.split("\r\n\r\n")
        ctype=contenttype(got[0].split("\r\n"))
        vals,code=security2(got[0].split("\r\n"))
        if verbose and vals!="":
            print("File Name : {}\nFile Type : {}".format(vals,ctype))
        
        if(len(got)<2):
            got.append("")
            
        try:
            if(code!="400 BAD REQUEST"):
                if(len(Path)<1):
                    file=open(vals,"w")
                    file.write(got[1])
                    file.close()
                else:
                    file=open(Path+"\\"+vals,"w")
                    file.write(got[1])
                    file.close()
            if verbose:
                print("File CREATED BY :"+address[0]+","+str(address[1]))

        except:
            code="404"


        file2=str(time.ctime(int(time.time())))
        return got[0].split("\r\n")[2:],got[1],code,file2    

            

  
def callget(value,Path):
    global code
    listt=[]
    file=""
    headers=[]
    fileread=""
    vals,code=security(value)
    fileread=""
    try:
        if(len(Path)<1):
            fileread=open(vals,"r").read()
        else:
            fileread=open(Path+"\\"+vals,"r").read()
        file2=str(time.ctime(int(time.time())))        
                
    except:
        code="404 NOT FOUND"
        file2=str(time.ctime(int(time.time())))

    
    listt=value[2:],fileread,code,file2
    return listt  
     
def listene(PORT):
        PORT=int(PORT)
        HOST = '127.0.0.1'
        if(verbose):
            print("Server Listning at Port: "+str(PORT))
            print("Server Host ID: "+HOST)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(verbose):
            print("Server Socket Connection Made")
        
        s.bind((HOST, PORT))
        s.listen(5)
        if(verbose):
            print("Server bind Complete\nServer Listning")
        return s
   
def work(conn,address,Path,verbose):
    recv=''
    answer=''
    
    while True:
        data = conn.recv(1024).decode()
        recv+=data
        
        if len(data)<1024:
         break
    typ1=recv.split("\r\n")
    typ=typ1[0].split(" ")[0].upper()
    if(typ=="GET"):
        value=  callget(typ1,Path)
        clen= len(recv)
        heading=myheader(value,clen)
        answer=heading+"\r\n\r\n"+value[1]
        
    elif(typ=="POST"):
        value=callpost(recv,Path,address)
        heading=myheader(value,len(value[1]))
        answer=heading+"\r\n\r\n"+value[1]
        
    else:
        print("INVALID REQUEST")
        val="","400 BAD REQUEST",[]
        answer=myheader(val,0)
        
    if verbose:
        print("SENDING ENCODED DATA")
    conn.sendall(answer.encode())
    if verbose:
        print("CLOSING CONNECTION")
    conn.close()
def processing(text):
    global verbose
    verbose=False
    Port=8081
    Path=""

    try:
        for i in range(len(text)):
            if(text[i][:1]=="-"):
                if(text[i]=="-v"):
                  verbose=True
                elif (text[i]=="-p"):
                    Port=text[i+1]
                elif(text[i]=="-d"):
                    Path=text[i+1]
    except:
         print("ERROR")

    return verbose,Path,Port
def main():
    print("Press enter for default port and path")
    lya=input("HTTP ")
    verbose=False
    Port=8081
    Path=""
    if(len(lya)>1):
        verbose,Path,Port=processing(lya.split(" "))
    s=listene(Port)
    if verbose:
        if(Path==""):
            print("Directory : DEFAULT")
        else:
            print("Directory : "+Path)
  
    while True:
        conn, address = s.accept()
        if verbose:
            print("\nNew Connection with : "+address[0])
            print("UNIQUE ID : "+str(address[1]))
        Thread(target=work, args=(conn, address,Path,verbose)).start()
    s.close()

main()
























    ####dd=value[0].split(" ")[1][1:]
    ####directory=os.listdir(dd)
    ####print(directory)
   # os.chdir(name_split)
##   if vals == "":
##            file = os.listdir()
##            file="\n".join(file)


