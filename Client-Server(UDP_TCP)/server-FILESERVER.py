import socket
import os
import time
from threading import Thread
verbose=False
def myheader(val,lenth):
    if verbose:
        print("CREATING HEADER...")
    txt1="HTTP/1.0 "+val[1]+"\r\n"
    date2="Date: "+str(time.ctime(int(time.time())))+"\r\n"
    con="Content-Lenth:"+str(lenth)+"\r\n"
    x=socket.gethostname()
    server="Server:"+x+"\r\n"
    txt2="Access-Control-Allow-Origin: *\r\n"
    txt3="Access-Control-Allow-Credentials: true\r\n"
    txt4="\r\n".join(val[2])
    if verbose:
        print("HEADER CREATED")
    return txt1+date2+con+server+txt2+txt3+txt4

def security(value):
    if verbose:
        print("CHECKING SECURITY FOR FILE REQUEST")
    vals=value[0].split(" ")[1][1:]
    if len(vals)<1:
        return "","200 OK"
    elif vals[0:3]=="../" or len(vals.split("/"))>1:
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
    vals,code=security(got[0].split("\r\n"))
    if verbose and vals!="":
        print("File Name : {}\nFile Type : {}".format(vals,ctype))
    if verbose and vals=="":
        print("DIRECTORY CONTENT REQUEST")
    

    if(len(got)<2):
       if verbose:
           print("NO INLINE DATA FOUND")
       got.append("")

 
    if len(vals)<=0:
        if verbose:
            print("Error File Name Empty")
        code="400 BAD REQUEST"
    try:
        if(code!="400 BAD REQUEST"):
            if(len(Path)<1):
                file=open(vals+"."+ctype,"w")
                file.write(got[1])
                file.close()
            else:
                file=open(Path+"\\"+vals+"."+ctype,"w")
                file.write(got[1])
                file.close()
            if verbose:
                print("File CREATED BY :"+address[0]+","+str(address[1]))

            
    except:
           code="ERROR CHECK DIRECTORY AND FILE"     

    return "",code,got[0].split("\r\n")[2:]  
    

def callget(value,Path):
    global code
    listt=[]
    file=""
    headers=[]
    if verbose:
        print("Request Type : GET request")
    ctype=contenttype(value)
    vals,code=security(value)
    fileread=""

    if verbose:
        print("File Name : {}\nFile Type : {}".format(vals,ctype))
    

    try:
     if(code!="400 BAD REQUEST"):  
        if(len(vals)<1):
            if verbose:
                print("Reading directory Content")
            if(len(Path)<1):
                fileread="\n".join(os.listdir())
            else:
                fileread="\n".join(os.listdir(Path))
        elif len(vals)>1:
            if verbose:
                print("Reading File Content")
            if(len(Path)<1):
                fileread=open(vals+"."+ctype,"r").read()
            else:
                fileread=open(Path+"\\"+vals+"."+ctype,"r").read()
                    
    except:
           code="404 NOT FOUND"     
           fileread=""
    listt=fileread,code,value[2:]
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
        head=myheader(value,len(value[0]))
        answer=head+"\r\n\r\n"+value[0]
    elif(typ=="POST"):
        val=callpost(recv,Path,address)
        answer=myheader(val,len(val[0]))
        
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
    Port=8080
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
    lya=input("HTTPFS ")
    verbose=False
    Port=8080
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
        print("abc")

    s.close()
    
main()

























#    if(len(vals)>1):
 #           code="200 OK"
  #          for i in fileread:
##if(vals == i.split(".")[0] and ctype==i.split(".")[1]):
    #                vals=i
   #         if(not len(Path)<1):
      #          Path=Path+"\\"
     #       fileread=open(Path+vals,"r").read()
  #  else:
   #         code="200 OK"
    #        fileread="\n".join(fileread)

    ####dd=value[0].split(" ")[1][1:]
    ####directory=os.listdir(dd)
    ####print(directory)
   # os.chdir(name_split)
##   if vals == "":
##            file = os.listdir()
##            file="\n".join(file)


