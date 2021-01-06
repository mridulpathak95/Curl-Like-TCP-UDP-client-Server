import socket

def request():
    request1="GET /"+args+" HTTP/1.0\r\nHost: "+name+"\r\n"+"\r\n".join(ht)+"\r\n\r\n"
    request2="POST /index2.html"+args+" HTTP/1.0\r\nHost: "+name+"\r\n"+"\r\n".join(ht)+"\r\n\r\ndatafatadfatatfdtw"
    return request1



HOST = '127.0.0.1'
PORT = 8080
args=""
name="mridul.xyz"
ht=["pazim:goyal","mridul:pathak","Content-Type:html","Mridul:Pathak","content-disposition:inline"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


request=request()
s.send(request.encode())
rec=''
while True:
    data = s.recv(1024).decode()
    rec+=data
    if  len(data)<1024:
        break

value=rec.split("\r\n")
cd="inline"
output=""
for i in value:
    if(i[0:12].lower()=="content-type"):
        output= i[13:].lower()
        break;
if output=="":
    output="txt"
fname="default"
for i in value:
    if(i[0:19].lower()=="content-disposition"):
        data=i[20:]
        cd=i[20:]
        data=data.split(",")
        if len(data)==2:
            fname=data[1]
if cd!="inline":
    f=open(fname+"."+output,"w")
    f.write(rec)
    f.close()
    print("SAVED")
else:
    print(rec)
