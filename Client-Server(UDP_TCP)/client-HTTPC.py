import socket
#Name of command line is Mridul ... you can use word mridul similar to curl

# variables 
verbose=False
save=False
filename=""
redirected=0


#--------------POST FUNCTION----------------------------------------    

def post(name,args,ht,inline,filetext):
  try:  
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    port=8080
    sock.connect((name,port))
    inline=inline.replace(":",": ")
#-----Error Handeling: If user Enters both file name and data (-d and -f)
    if(len(inline) > 0 and len(filetext) >0):
     print("Both Inline data and File Cant be used together \nWe Eliminated the File Data and using just Inline Data\n\n ")
    elif(len(filetext)>1):
        inline=filetext
    
    if(len(ht)==0):
        headers=""
    else:
        headers="\r\n"+"\r\n".join(ht)
    request="POST /"+args+" HTTP/1.0\r\nHost: "+name+"\r\nContent-Length: "+str(len(inline))+headers+"\r\n\r\n"
    sock.sendall(request.encode()+inline.encode())
    results = ''
    while True:
      recv = sock.recv(1024).decode()
      if not recv:
        break
      results += recv
    return results
  except:
        print("Something went wrong .\nPlease Check Input and make sure network is connected. You can try again")
      

#--------------GET FUNCTION----------------------------------------    

def get(name,args,ht):
 try:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    port=8080
    sock.connect((name,port))
  
    request="GET /"+args+" HTTP/1.0\r\nHost: "+name+"\r\n"+"\r\n".join(ht)+"\r\n\r\n"
    sock.send(request.encode())
    results = 'mridul'

    while True:
      recv = sock.recv(1024).decode()
      if  not recv:
        break
      results =results + str(recv)
    return results
 except:
        print("Something went wrong .\nPlease Check Input and make sure network is connected. You can try again")

#----------------------PROCESSING OF COMMAND--------------------------------    
   
def processing(text):
 try:
  global verbose
  global save

  global filename
  headertext=[]
  inlinetext=""
  filetext=""
  url=""

  for i in range(1,len(text)):
    if(text[i][:1]=="-"):
      if(text[i]=="-v"):
        verbose=True
      if(text[i]=="-h"):
        if(":" not in text[i+1]):
            print("Header Format not .. Invalid Request...  Removing Header")
        else:    
            headertext.append(text[i+1])
      if(text[i]=="-d"):
        if(text[i+1][:1]!="-"):  
            inlinetext=text[i+1]
        else:            
            print("InlineData Format not .. Invalid Request...  Removing Header")
      if(text[i]=="-f"):
          filetext=open(text[i+1],"r").read()
      if(text[i]=="-o"):
        save=True
        filename=text[i+1]
    elif((("." in text[i]) and (text[i-1][:1]!="-")) or (("." in text[i]) and (text[i-1]=="-v"))):
      url=text[i]

  oururl=urledit(url)
  
  callingmethods(text,oururl,headertext,inlinetext,filetext)
 except:
        print("Something went wrong .\nPlease Check Input and make sure network is connected. You can try again")

#--------------------HELP METHOD---------------------------------
def help():
    print("Curl like commandline. Comp 6461\nTo use the  command Enter command starting in following way:\n[anyword] GET/POST [-v] ([-h] key:value) ([-d] inlinedata) [URL] [-o file name]\n -d : For HTTP POST data \n -f : Sending POST data from a File\n -h : For passing custom header line to server(could be multiple lines)\n -o : Write to a text file instead of standard output\n -v : verbose Prints the response of website including protocols, status and headers\n")
    
def helpget():
    print(" To use the  command for GET\n Enter command starting in following way:\n [anyword] GET [-v] ([-h] key:value) [URL] [-o file name]\n -h : For passing custom header line to server(could be multiple headers)\n -o : Write the output to a text file instead of standard output\n -v : verbose Prints the response of website including protocols, status and headers\n")
    
def helppost():
    print("To use the  command for POST\n Enter command starting in following way:\n [anyword] POST [-v] ([-h] key:value) ([-d] inlinedata) [URL] [-o file name]\n -d, --data, --DATA : For HTTP POST data \n -f : Sending POST data from a File\n -h : For passing custom header line to server(could be multiple lines)\n -o : Write to a text file instead of standard output\n -v : verbose Prints the response of website including protocols, status and headers\n")
    
    
        




#---------------METHOD THAT CALLS GET OR POST-------------------------
    
def callingmethods(text,oururl,headertext,inlinetext,filetext):
    global redirected
    if(text[1]=="get" or text[1]=="GET" or text[1]=="Get"):  
        results=get(oururl[0],oururl[1],headertext)
        abc= chk301(results)
 #-----------------ERROR HANDELING URL REDIRECT and count       
        if(abc is not None):
            if(abc[0:7]=="http://" or abc[0:8]=="https://" ):
                oururl=urledit(abc)
            else:
                oururl[1]=abc
            if(redirected<5):

                redirected=redirected+1           
                callingmethods(text,oururl,headertext,inlinetext,filetext)
            else:
                print("Too Many Redirects")

    elif(text[1]=="help" or text[1]=="HELP"or text[1]=="Help"):
        try:
            if text[2]=="get" or text[2]=="GET" or text[2]=="Get" :helpget()
            elif text[2]=="post" or text[2]=="POST"or text[2]=="Post":helppost()
            else:
                help()
        except:
            help()
        
    elif(text[1]=="post" or text[1]=="POST" or text[1]=="Post"):
        results=post(oururl[0],oururl[1],headertext,inlinetext,filetext)
        abc=chk301(results)
        if(abc is not None):
            if(abc[0:7]=="http://" or abc[0:8]=="https://" ):
                oururl=urledit(abc)
            else:
                oururl[1]=abc
            if(redirected<5):
                redirected=redirected+1
                callingmethods(text,oururl,headertext,inlinetext,filetext)
            else:
                print("Too Many Redirects")
        
    else:
        print("Something went wrong .\nPlease Check Input and make sure network is connected. You can try again")
#----------------ERROR HANDELING : REMOVING HTTP:// if inserted----------------------------------------------------    
def urledit(url):
  if(url[0:7]=="http://"):
      url=url[7:]
  if(url[0:8]=="https://"):
      url=url[8:]
      
#----------------ERROR HANDELING : IF JUST HOST IS PROVIDED WITHOUT PATH
  oururl=url.split("/",1)
  if len(oururl)<2:
      oururl.append("")
  return oururl
#------------------VERBOSE AND SAVE FILE FUNCTION--------------------------------------------------
def afterresults(results):
    if(verbose):        
       print(results)
    else:
      if(len(results.split("\n\r",1)[1])>1):  
        print(results.split("\n\r",1)[1])
      else:
          print(results)
    if(verbose and save):
      f=open(filename,"w")
      f.write(results)
      print("File Saved as : "+filename)
    elif(save):
      f=open(filename,"w")
      f.write(results.split("\n\r",1)[1])
      print("File Saved as : "+filename)

  
#-----------------------FUNCTION REDIRECTION---------------------------------------------
def chk301(results):
 
 try:
    newurl=""
    if(list(results.split("\n",1)[0].split(" ")[1])[0]=="3"):
        print("\nPage Permanently moved.")
        head=results.split("\n\r")[0].split("\n")
        newurl=""

        for i in head :
            if(i[:9]=="Location:"):
                newurl=i[10:]
                newurl=newurl[:len(newurl)-1]
                break
        print("Redirecting to : "+newurl)    
        return newurl
    else:

        afterresults(results)
 except:
     print("Something went wrong .\nPlease Check Input and make sure network is connected. You can try again")
#--------------------------------------------------------------------
def main():
    url1="Pazim get 127.0.0.1/file.html -h Content-Type:html -h keep:alive"
    url2="Pazim get -v -h Keep-Alive:10 -h Accept-language:en -h Content-Type:html 127.0.0.1/file2"
    url3="Pazim get -v -h Keep-Alive:10 -h Accept-language:en -h Content-Type:html -h Content-Disposition:save,newtempfile 127.0.0.1/file2"
    url4="Pazim post -v -d userName=PAZIM_MRIDUL&password=GOYAL_PATHAK httpbin.org/post -o temp.txt"
    url5='Pazim post -v -h Content-Type:application/json -d {"Assignment": 1} http://httpbin.org/post -o temp.txt'
    url6="Pazim post -v -h Content-Type:application/json -h Keep-Alive:10 -h Accept-language:en -f file.json httpbin.org/post -o temp.txt"
    url7="Pazim post -v -h Content-Type:text/html -h Keep-Alive:10 -h Accept-language:en -f file2.html httpbin.org/post  -o temp.txt"
    url8="Pazim get -v -h Content-Type:text/html -h Keep-Alive:10 -h Accept-language:en concordia.ca -o temp.txt"
    url9="Pazim get -v -h Content-Type:text/html -h Keep-Alive:10 -h Accept-language:en httpbin.org/redirect/7 -o temp.txt"
    url10="Pazim Help Get"
    inputs=input("\nSelect options 1 - 10 or enter anything else to enter command manually\n\n1). GET without VERBOSE or HEADER\n   "+url1+"\n\n2). GET with VERBOSE and HEADER\n   "+url2+"\n\n3). GET with VERBOSE and save output in text file (Server: http://www.mridul.xyz)\n   "+url3+"\n\n4). POST with VERBOSE and Data Sent is form type in inline data\n   "+url4+"\n\n5)POST with VERBOSE and INLINE data in form of JSON and output saved in text file\n   "+url5+"\n\n6). POST with VERBOSE and data from JSON FILE and output saved in text file\n   "+url6+"\n\n7). POST command data from a file and type HTML\n   "+url7+"\n\n8).  GET command to a URL Permanently Moved - Error Code 3XX (Server Concordia.ca ::- permanently moved to www.concordia.ca)\n   "+url8+"\n\n9).  GET command to a URL Permanently Moved - Error Code 3XX (More then 6 times) (Server:  httpbin.org/redirect/6 ::- permanently moved to httpbin.org/get) \n"+url9+"\n\n10). Pazim Help Get \n"+url10+"\n\nEnter Any thing Else to Enter Command Manually \n ")


    if(inputs=="1"):
            url=url1
    elif(inputs=="2"):
            url=url2
    elif(inputs=="3"):
            url=url3
    elif(inputs=="4"):
            url=url4
    elif(inputs=="5"):
            url=url5
    elif(inputs=="6"):
            url=url6
    elif(inputs=="7"):
            url=url7
    elif(inputs=="8"):
            url=url8
    elif(inputs=="9"): 
            url=url9
    elif(inputs=="10"):
            url=url10
    else:
            url=input("Enter command starting in following way:\n[anyword] GET/POST/HELP [-v] ([-h] key:value) ([-d] inlinedata) [URL] [-o file name]\n")
    url=url.replace(": ",":")
    text=url.split(" ")
    processing(text)
    exits=input("\n\nDo You want to run the program again. Press Y for Yes and anything for no\n")
    if(exits=="Y" or exits=="y"):
        global redirected
        redirected=0
        main()
    else:
        exit() 
main()
