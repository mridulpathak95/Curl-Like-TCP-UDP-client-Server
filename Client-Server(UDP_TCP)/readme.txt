SERVER-HTTP :
http server running on port 8081
the server responds to http requests i.e get and post request
the server runs continuesly and can handle multiple clients

get returns the requested file , returns index.html if url is just host name and 404 otherwise
post saves the inline data in file and returns the same data with appropriate header


SERVER-FILESERVER:
http server running on port 8080
the server responds to http requests i.e get and post request
the server runs continuesly and can handle multiple clients

implimentations- 
GET/
GET/foo
POST/foo

Error handling and Security

file name is "foo" and file type is given in "Content-Type:xx" and is ".txt" as default
file is displayed with header if return header contains Content-disposition:inline and save the data tofile if Content-Disposition:attachment /attachment,filename 


CLIENT HTTP is curl like commandline work for both servers but on different port
CLIENT FILESERVER is simple get and post request that work on both servers on different ports and also implimentr content disposition